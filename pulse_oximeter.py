# Pulse Oximeter Software
# Hardware: Raspberry Pi Pico, SSD1306 OLED
# Display, Red/IR diodes, Phototransistor
# Author: Maciej Otwiaska, Bartosz Piotrowski
# Version: 2.0
# Date: 16.12.2024
# Description: This program measures light intensity
# using a phototransistor, calculates SpO₂ and BPM,
# and displays the results on an OLED screen.

from machine import Pin, ADC, I2C
import ssd1306
import time

# Initialization

# Initialize GPIO pins for Red and IR LEDs
# Red LED for 660 nm light, IR LED for 940 nm light
red_led = Pin(21, Pin.OUT)
ir_led = Pin(20, Pin.OUT)

# Initialize ADC pin for phototransistor
# Reads light intensity from Red and IR LEDs
phototransistor = ADC(26)

# Initialize I2C interface for OLED display
# SCL = Pin 5, SDA = Pin 4
i2c = I2C(0, scl=Pin(5), sda=Pin(4))
oled_width = 128  # Width of OLED display in pixels
oled_height = 64  # Height of OLED display in pixels
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# Graph parameters for visualizing signal data on OLED
graph_width = oled_width - 20
graph_height = (oled_height - 20) // 2

# Define the expected ranges of light intensity for Red and IR LEDs
red_min_value = 700
red_max_value = 14000
ir_min_value = 500
ir_max_value = 1300

# Buffers and Variables

# Buffers to store recent signal data for processing
data_buffer_red = [0] * 100  # Red light intensity
data_buffer_ir = [0] * 100  # IR light intensity
data_buffer_redg = [0] * graph_width  # Red graph data
data_buffer_irg = [0] * graph_width  # IR graph data

# Variables for SpO₂ and BPM calculations
last_peak_time = 0
current_time = 0
pulse = 0  # Beats per minute (BPM)
spo2 = 0  # Blood oxygen saturation (SpO₂)
counter = 0
threshold = 0  # Dynamic threshold for detecting peaks
current_peak = 0
peak_stop_time = 0
peak_start_time = 0


# Functions

# Function to calculate dynamic threshold for peak detection
# Threshold is set as the average of the maximum and minimum values in the buffer
def set_threshold(buffer):
    avg = ((max(buffer) + min(buffer)) // 2)
    return avg


# Function to calculate SpO₂ based on the ratio
# of red to IR light absorption
# This uses an empirical formula to approximate oxygen saturation
def calculate_spo2(red_value, ir_value):
    if ir_value == 0:  # Avoid division by zero
        return 0
    ratio = (red_value / red_max_value) / (ir_value / ir_max_value)
    return 110 - (25 * ratio)


# Function to normalize light intensity values for graphical display
# Maps the raw value to a fixed range (e.g., graph height)
def normalize(value, min_value, max_value, scale):
    return int((value - min_value) / (max_value - min_value) * scale)


# Main Loop

# Continuously read signals, calculate BPM/SpO₂,
# and update the OLED display
while True:
    # 1. Measure light intensity for Red LED
    red_led.on()  # Turn on Red LED
    time.sleep(0.005)  # Wait for phototransistor to stabilize
    red_value = phototransistor.read_u16()  # Read Red light intensity
    red_led.off()  # Turn off Red LED

    # 2. Measure light intensity for IR LED
    ir_led.on()  # Turn on IR LED
    time.sleep(0.005)  # Wait for phototransistor to stabilize
    ir_value = phototransistor.read_u16()  # Read IR light intensity
    ir_led.off()  # Turn off IR LED

    # 3. Clip raw sensor readings to defined ranges
    red_value_clipped = max(red_min_value, min(red_max_value, red_value))
    ir_value_clipped = max(ir_min_value, min(ir_max_value, ir_value))

    # 4. Normalize sensor readings for graphical display
    normalized_red = normalize(red_value_clipped, red_min_value, red_max_value, graph_height)
    normalized_ir = normalize(ir_value_clipped, ir_min_value, ir_max_value, graph_height)

    # 5. Update rolling buffers for signal data
    # These buffers store recent data for processing and graphing
    data_buffer_red.pop(0)
    data_buffer_red.append(red_value)
    data_buffer_ir.pop(0)
    data_buffer_ir.append(ir_value)
    data_buffer_redg.pop(0)
    data_buffer_redg.append(normalized_red)
    data_buffer_irg.pop(0)
    data_buffer_irg.append(normalized_ir)

    # 6. Calculate dynamic threshold every 50 iterations
    counter += 1
    if counter > 50:
        threshold = set_threshold(data_buffer_red)  # Update threshold based on recent data
        counter = 0

    # 7. Detect peaks in Red light signal
    # Peaks represent heartbeats for BPM calculation
    if data_buffer_red[-1] > (threshold + ((max(data_buffer_red) - threshold) // 3)) and current_peak == 0:
        peak_start_time = time.ticks_ms()  # Record start time of the peak
        current_peak = 1  # Mark the peak as detected

    if data_buffer_red[-1] < (threshold - ((max(data_buffer_red) - threshold) // 3)) and current_peak == 1:
        peak_stop_time = time.ticks_ms()  # Record stop time of the peak
        current_peak = 0  # Mark the end of the peak

    # 8. Calculate SpO₂ and BPM
    spo2 = calculate_spo2(red_value_clipped, ir_value_clipped)  # SpO₂ based on absorption ratio
    if peak_stop_time - peak_start_time > 0:  # Ensure valid time interval
        pulse_try = int(60 / ((peak_stop_time - peak_start_time) / 1000))  # Calculate BPM
        if 40 < pulse_try < 160:  # Filter unrealistic BPM values
            pulse = pulse_try

    # 9. Update OLED display with results and graphs
    oled.fill(0)  # Clear the screen
    oled.text("Pulse: {} bpm".format(pulse), 0, 0)  # Display BPM
    oled.text("SpO2: {:.1f}%".format(spo2), 0, 10)  # Display SpO₂

    # Display Red light graph
    oled.text("RD", 0, graph_height + 8)
    for x in range(graph_width):
        y = graph_height - data_buffer_redg[x]
        oled.pixel(x + 20, y + 16, 1)

    # Display IR light graph
    oled.text("IR", 0, oled_height - 8)
    for x in range(graph_width):
        y = oled_height - 1 - data_buffer_irg[x]
        oled.pixel(x + 20, y, 1)

    oled.show()  # Refresh the display to show updated content

    # 10. Wait briefly before next reading
    time.sleep(0.05)

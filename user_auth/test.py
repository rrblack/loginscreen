import pyautogui
import time

# Give yourself a few seconds to switch to the typing test window
time.sleep(6)

text = "Four score and seven years ago our fathers brought forth on this continent a new nation, conceived in liberty, and dedicated to the proposition that all men are created equal. Now we are engaged in a great civil war, testing whether that nation, or any nation, so conceived and so dedicated, can long endure. We are met on a great battlefield of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do thtis,."  # Replace with actual test text
pyautogui.typewrite(text, interval=0.067)  # Types each character with a slight delay

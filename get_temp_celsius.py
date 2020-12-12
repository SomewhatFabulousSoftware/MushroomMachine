import mcp9600
import time
m = mcp9600.MCP9600(0x66)
temp_c = m.get_hot_junction_temperature()
print(temp_c)

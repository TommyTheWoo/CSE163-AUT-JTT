"""
Analyzes the relationship between public transit ridership
and vehicle registration by fuel type.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ruggedness_stats as rs
import vehicle_registration_data as vrd

terrain_data = rs.main()
vehicle_data = vrd.main()

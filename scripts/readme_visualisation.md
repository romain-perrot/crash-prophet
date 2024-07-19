From the main histogram obtained:

- Road type feature: majority accident in single carriageway followed by dual warriageway, and then roundabout.
- Junction control feature: huge number of NaN (is that means there is no possibilities to describe it ?), and Giveway or uncontrolled, followed by automatic traffic signal
- Pedestrian crossing human control feature: Most of them are None within 50m (can be removed)
- Pedestrian crossing facilities feature: Most of them no physical crossing within 50m (can be removed)
- Light conditions: most accidents occur when there is daylight (+ street light present) -> logic as most of accidents occur during the day followed by darkness with street - lights present and lit, small number for no street lighting
- Weather conditions feature: Most of them is fine without high winds followed by raining without high winds
- Road surface conditions feature: Most of the time the road is dry, followed by wet/damp
- Special conditions at site feature: can be removed as most of values are nan
- Carriage hazards feature: can be removed as most of values are nan

Hour vs Day stacked bar:
- Overall, accidents occur with the highest number at 8AM and 5PM which correspond to rush hours during the week.
- From Monday to Friday the majority of accidents occur the day from 7AM to 7PM.
- During week ends the accidents are mostly during the afternoon.
- The evening/night accidents mostly occur during Saturdays/Sundays

Month vs Weather Conditions:
- Most of the year the weather is fine without high winds, followed by raining without high winds
- There is snow from November to March
- Small proportions of other or unknown weather
- Small proportion of fine weather with high winds

Road Conditions vs Weather Conditions:
- When weather is fine without high winds, the road condition is mostly dry, followed wet/damp, and finally, frost/ice
- When the weather is raining without high winds, the road condition is wet/damp
- When the weather is unknown it is almost always dry

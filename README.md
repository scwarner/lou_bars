# The Louisville Bars Bar Chart
Louisville is known as a fun-loving town. The Highlands section of the city is especially known for its restaurants, bars and other nightlife. Best is it really the best area for a night out on the town?

To answer this question, I analyzed ABC License Data from the Louisville Open Data website to see which sections of the city had the highest number of bars. I measured this using the ZIP code column in the CSV. Though the boundaries do not perfectly match, I considered the 40204 and 40205 ZIP codes as the Highlands. 

My research led to a deep, philosophical question: What is a bar? Based on the ABC License Data, that question is not so easy to answer. Some establishments that a person might consider to be a bar (the Haymarket Whiskey Bar, for example) are categorized as restaurants in the CSV, even if they have limited food offerings. Other establishments that offer extensive food menus are listed as bars. 

To get as accurate of a number as possible, I wrote a SQL query that selected not only establishments with a SubDescription of "Bar" but establishments that had "Bar", "Tavern" or "Pub" in their names. I also included breweries in my search. I grouped the results by ZIP code and ordered them from the highest number of bars to the lowest.

Louisville has a total of 36 ZIP codes, so to make my visualization more manageable, I limited the results to the 10 ZIP codes with the highest number of bars. Overall, the 40202 ZIP code, which comprises downtown and part of Nulu, has the highest number of bars at 35. However, the combined 40204 and 40205 ZIP codes exceeds that number at 38.

A bar chart seemed the most appropriate tool to visualize the data, so I used Bokeh to create the plot and show the results.
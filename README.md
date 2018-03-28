# The Louisville Bars Bar Chart
Louisville is known as a fun-loving town. The Highlands section of the city is especially known for its restaurants, bars and other nightlife. Best is it really the best area for a night out on the town?

To answer this question, I analyzed ABC License Data from the Louisville Open Data website to see which section of the city had the highest number of bars. My hunch was that it would be the Highlands, of course. After all, it ***is*** the home of the fabled Bambi Walk.

This was not as straight forward of a task as I imagined. First, I had to consider a deep, philosophical question: What is a bar? According to Merriam-Webster, a bar is "a room or establishment where alcoholic drinks and sometimes food are served." I think that is a good, clear definition, but that is not necessarily how the ABC License Data CSV defines a bar. Some establishments that a person might consider to be a bar (the Haymarket Whiskey Bar, for example) are categorized as restaurants in the CSV, even if they have limited food offerings. Other establishments that offer extensive food menus are listed as bars, including Magnolia 610 and the Blue Dog Bakery. 

To get as accurate of a number as possible, I wrote a SQL query that selected not only establishments with a SubDescription of "Bar" but establishments that had "Bar", "Tavern" or "Pub" in their names. (If you call yourself a bar, then I'll take your word for it.) I also included microbreweries in my search.   

Second, I had to determine how to best represent the various sections of the city.

A bar chart seemed the most appropriate tool to visualize the data, so I used Bokeh to create the plot and show the results.
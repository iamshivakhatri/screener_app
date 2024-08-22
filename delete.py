from datetime import datetime
from pytz import timezone

barset= api.get_barset( 'DIA', '1Min', limit = 5 ).df
display(barset)

market_timezone = timezone('America/New_York')
current_time = datetime.now(market_timezone)
display('{:%Y-%m-%d %H:%M:%S} is the current time'.format(current_time))

last_bar_time = barset.index.max()
delta_time = current_time - last_bar_time
delta_time_sec = delta_time.total_seconds() % 60
delta_time_min = delta_time.total_seconds() // 60
display('delta time is {:.0f} min {:.0f} sec'.format(delta_time_min, delta_time_sec))
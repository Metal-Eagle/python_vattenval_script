    
import get_tokens
import get_data
import post_data

# update tokens and save tokes
get_tokens.get_token()


# get hours_data and post to API
get_data.hours_data()
post_data.post_hours()

# get days_data and post to API
get_data.days_data()
post_data.post_days()


# get months_data and post to API
get_data.months_data()
post_data.post_months()



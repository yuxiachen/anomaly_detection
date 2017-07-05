# anomaly_detection

1. Files includes with this project:

├── README.md 
├── run.sh
├── src
│   └── main.py
│   └── detector.py
│   └── social_network.py
├── log_input
│   └── batch_log.json
│   └── stream_log.json
├── log_output
|   └── flagged_purchases.json
├── insight_testsuite
    └── run_tests.sh
    └── tests
        └── test_1
        │   ├── log_input
        │   │   └── batch_log.json
        │   │   └── stream_log.json
        │   |__ log_output
        │       └── flagged_purchases.json
        ├── my-own-test
            ├── log_input
            │   └── batch_log.json
            │   └── stream_log.json
            |__ log_output
                └── flagged_purchases.json     
2. Design Decisions:
The Detector class is implemented to built a detector with initial input data. The event_process method is not only used to update the user social network and the purchase during the initial process and following analysis process, but also used to analize the following coming purchase records to check if it is an anomaly based on the initial data.
The SocialNetwork class is implemented to built a social network of users. The methods of add_user, update_network is implemented in the SocialNetwork Class tof map and update the users and their relations. While the methods of update_purchase and get_tracked_purchases is implemented to update the purchase history of a given user and get the latest given number of purchase history of a given user's social network defined by a given degree.

3. Algorithm Analysis Results
The search algorithms I implemented was the get_tracked_purchases. Its run time is o(T*k). T is the tracked number of purchase. K is the friend number in degree of a given user. I added a counter to stamp the input order of the records to assist the ranking of those purchase records which have the same timestamp. 
In the add_purchase, a deque is used to save the memory usage. The number of stored purchase history for a user is limited up to the number of tracked purchases.

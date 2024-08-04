My App is a Software Assistant, which provides software installation guidelines and further installation support.

It is more user friendly, a beginner can also easily download and install the requested software without any support from the IT team.

I designed this app in a business point of view, in an organization, IT people were burdened with lot of support works, in that the major work is providing software assistance, to reduce their burden and to increase their productivity, I created this app

My app uses a RAG based employee validation, which gets the employee id and the requested software from the Employee and validates the employee is present in the organization and checks the access of the requested software.

If the employee has the access to the requested software, the assistant will provide installation guide, if the employee face any installation issue, the app provides further support. If the employee don't have the access to the requested software, it returns invalid access.

I have used Gemini-1.5-Pro for installation guidelines and further support with incremental chat history learning mechanism. The model uses its pretrained data to provide the installation guide and support.

I have developed this app as a Python flask app with assistance of HTML, CSS and JavaScript for UI

The main aim of this app is to provide step by step, beginner and user friendly installation guideline to the end user, which reduces the burden of the IT people. 

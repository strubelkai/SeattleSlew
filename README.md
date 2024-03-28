Background: [Equine Lung Experts](https://www.equinelungexperts.com/) is a diagnostic labs service. Veterinary diagnostic laboratories don't have the specialized knowledge in equine pulmonology to accurately diagnose respiratory diseases based on bronchoalveolar lavage fluid cytology samples. As leading specialists in horse asthma (heaves, RAO, IAD, COPD, and chronic bronchitis), exercise-induced pulmonary hemorrhage 
(EIPH or epistaxis), and other respiratory diseases affecting performance, we provide in-depth evaluations of pulmonary health and risk factors. 

Project: Today this process of gathering samples, mailing them in for analysis and returning to customer is very manually intensive. A simple cloud hosted web app would greatly streamline the process.

[Demo](https://www.youtube.com/watch?v=LJqrXAxcLzY)

![image](https://github.com/strubelkai/SeattleSlew/assets/122396447/9a9090eb-fbaf-419f-9b7a-5de50e50df68)


Django Web Application hosted on Azure App Service:
-  Allows user to upload photo to be stored in cloud storage (Azure Blob)
- Captures some information via a form to be stored in a db (Cosmos Db)
- Runs model to label and identify cells (BALF cytology results) saving image to Azure Blob (To Do: use function app to run this analysis async on submission)

Azure Function App: 
- Asynchronous job that processes uploaded image and run against hosted YOLO model (TO DO unclear which ML service we'll use to host the model)
- Stores results in db to view in web application


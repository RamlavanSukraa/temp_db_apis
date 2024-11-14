##########################################################
#                                                        #
#  Auth:       Sukraa Software Solutions                 #
#  Created:    11/06/2024                                #
#  Project:    Prescription AI Agent                     #          
#                                                        #
#  Summary:    This project handles CRUD operations and  #
#              insights for prescriptions using MongoDB. #
#              It allows for the retrieval, creation,    #
#              update, and deletion of prescription      #
#              records, along with data filtering,       #
#              analysis, and summary insights.           #
#                                                        #
##########################################################

from fastapi import FastAPI
from routes.add_pres import router as add_pres_router


# Create FastAPI app
app = FastAPI()

# Include routes from separate files
app.include_router(add_pres_router,tags=['Mongo DB APIS'])

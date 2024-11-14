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
from routes.update_pres import router as update_pres_router
from routes.delete_pres import router as delete_pres_router
from routes.get_pres_id import router as get_pres_id_router
from routes.list_pres import router as list_pres_router
from routes.insights_pres import router as insights_pres_router

# Create FastAPI app
app = FastAPI()

# Include routes from separate files
app.include_router(add_pres_router,tags=['Mongo DB APIS'])
app.include_router(update_pres_router,tags=['Mongo DB APIS'])
app.include_router(delete_pres_router,tags=['Mongo DB APIS'])
app.include_router(get_pres_id_router,tags=['Mongo DB APIS'])
app.include_router(list_pres_router,tags=['Mongo DB APIS'])
app.include_router(insights_pres_router,tags=['Mongo DB APIS'])

from decouple import config
import dotenv
dotenv.load_dotenv(override=True)

class ConfigDev:
    SECRET_KEY = config('SECRET_KEY_DEV')
    MONGO = config('DB_MONGO_DEV')
    PORT = config('PORT_DEV')
    JWT = config('JWT_KEY_DEV')
    JWT_HRS = config('JWT_HRS_DEV')
    DEBUG = config('DEBUG_DEV')

# Configuración de producción
class ConfigProd:
    SECRET_KEY = config('SECRET_KEY')
    MONGO = config('DB_MONGO')
    PORT = config('PORT')
    JWT = config('JWT_KEY')
    JWT_HRS = config('JWT_HRS')
    DEBUG = config('DEBUG')
    
def get_config():
    environment = config('ENV', default='development')
    print(f" -------- Environment detected --------: {environment}")
    if environment == 'production':
        return ConfigProd
    return ConfigDev

current_config = get_config()
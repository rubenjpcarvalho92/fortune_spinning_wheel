from flask_sqlalchemy import SQLAlchemy

# Inicialização do SQLAlchemy
db = SQLAlchemy()

from .maquina import MaquinaModel
from .stock import StockModel
from .talao import TalaoModel
from .premio import PremioModel
from .cliente import ClienteModel
from .funcionario import FuncionarioModel
from .admin import AdminModel
from .login import LoginModel
from .levantamento import LevantamentoModel
from .setup import SetupModel


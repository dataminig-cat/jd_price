from logger import getMyLogger
from views import Main

itf = Main()
getMyLogger(itf.dfm)
itf.mainloop()


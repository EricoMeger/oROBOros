from i2clibraries import i2c_hmc5883l

bussola = i2c_hmc5883l.i2c_hmc5883l(1)

while True:
    bussola.setContinuousMode()
    bussola.setDeclination(x, x)
    lmao = bussola.getHeading()
    
    print(bussola)


#https://stackoverflow.com/questions/46902357/error-loading-mysqldb-module-did-you-install-mysqlclient-or-mysql-python
# Install mysqlclient  for usage with mysql
import pymysql

pymysql.install_as_MySQLdb()
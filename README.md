docker run --name mysql -v /mysql_data:/var/lib/mysql -e "MYSQL_ROOT_PASSWORD=123456" -p 3306:3306 -d mysql



Requirements
- Install Postgresql if i
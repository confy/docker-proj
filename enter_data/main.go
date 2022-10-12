package main

import (
	"bytes"
	"database/sql"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"

	"github.com/asmcos/requests"
	_ "github.com/go-sql-driver/mysql"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

//
func GetSqlDB(user string, pass string, host string, port string, database string) *sql.DB {
	var err error
	dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s", user, pass, host, port, database)
	sqldb, err := sql.Open("mysql", dsn)
	if err != nil {
		panic(err.Error())
	}
	return sqldb
}

func main() {

	AUTH_HOST := os.Getenv("AUTH_HOST")
	AUTH_PORT := os.Getenv("AUTH_PORT")
	DB_HOST := os.Getenv("DB_HOST")
	DB_DATABASE := os.Getenv("DB_DATABASE")
	DB_PORT := os.Getenv("DB_PORT")
	DB_USER := os.Getenv("DB_USER")
	DB_PASS := os.Getenv("DB_PASS")

	db := GetSqlDB(DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_DATABASE)

	fmt.Print(db)
	e := echo.New()
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.File("/", "www/index.html")

	e.POST("/data", func(c echo.Context) error {
		username := c.FormValue("username")
		password := c.FormValue("password")
		// start_timestamp := c.FormValue("start_timestamp")
		// end_timestamp := c.FormValue("end_timestamp")
		// minimum_heart_rate := c.FormValue("minimum_heart_rate")
		// peak_heart_rate := c.FormValue("peak_heart_rate")
		// calories_burned := c.FormValue("calories_burned")

		auth_url := fmt.Sprintf("http://%s:%s", AUTH_HOST, AUTH_PORT)
		auth_post_body, _ := json.Marshal(map[string]string{
			"username": username,
			"password": password,
		})
		resp, err := requests.PostJson(auth_url, auth_post_body)
		// return post(auth_post_body, auth_url, c)
		fmt.Print(resp, err)
		return err
	})

	httpPort := os.Getenv("HTTP_PORT")
	if httpPort == "" {
		httpPort = "8080"
	}

	e.Logger.Fatal(e.Start(":" + httpPort))
}

func newFunction(auth_post_body []byte, auth_url string, c echo.Context) error {
	responseBody := bytes.NewBuffer(auth_post_body)
	auth_resp, err := http.Post(auth_url, "application/json", responseBody)

	if err != nil {
		log.Fatalf("An Error Occured %v", err)
	}

	if auth_resp.StatusCode != 200 {
		return c.String(http.StatusUnauthorized, "Unauthorized")
	}

	defer auth_resp.Body.Close()

	body, err := ioutil.ReadAll(auth_resp.Body)
	if err != nil {
		log.Fatalln(err)
	}
	sb := string(body)
	log.Printf(sb)
	return c.String(http.StatusOK, sb)
}

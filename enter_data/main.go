package main

import (
	"bytes"
	"database/sql"
	"encoding/json"
	"io/ioutil"
	"log"
	"net/http"
	"os"

	_ "github.com/go-sql-driver/mysql"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func GetSqlDB() *sql.DB {
	var err error
	dbUser := "root" // mysql username
	dbPass := "root" // mysql password
	dbName := "godb" // mysql dbname
	sqldb, err := sql.Open("mysql", dbUser+":"+dbPass+"@/"+dbName)
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

	var sqldb *sql.DB

	e := echo.New()
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.File("/", "www/index.html")

	e.POST("/data", func(c echo.Context) error {
		username := c.FormValue("username")
		password := c.FormValue("password")
		start_timestamp := c.FormValue("start_timestamp")
		end_timestamp := c.FormValue("end_timestamp")
		minimum_heart_rate := c.FormValue("minimum_heart_rate")
		peak_heart_rate := c.FormValue("peak_heart_rate")

		auth_url := "http://" + AUTH_HOST + ":" + AUTH_PORT
		auth_post_body, _ := json.Marshal(map[string]string{
			"username": username,
			"password": password,
		})

		responseBody := bytes.NewBuffer(auth_post_body)

		auth_resp, err := http.Post(auth_url, "application/json", responseBody)

		if err != nil {
			log.Fatalf("An Error Occured %v", err)
		}

		if auth_resp.StatusCode != 200 {
			return c.String(http.StatusUnauthorized, "Unauthorized")
		}

		defer auth_resp.Body.Close()

		// If 200 our credentials are valid
		//Read the response body
		body, err := ioutil.ReadAll(auth_resp.Body)
		if err != nil {
			log.Fatalln(err)
		}
		sb := string(body)
		log.Printf(sb)
		return c.String(http.StatusOK, sb)
	})

	httpPort := os.Getenv("HTTP_PORT")
	if httpPort == "" {
		httpPort = "8080"
	}

	e.Logger.Fatal(e.Start(":" + httpPort))
}

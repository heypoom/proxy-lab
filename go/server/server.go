package main

import (
	"fmt"
	"log"
	"net/http"
)

func HelloHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Printf("accessing /%s\n", r.URL.Path[1:])

	fmt.Fprintf(w, "Hello, %s", r.URL.Path[1:])
}

func main() {
	log.Printf("Starting server at :1112")
	http.HandleFunc("/", HelloHandler)
	http.ListenAndServe(":1112", nil)
}


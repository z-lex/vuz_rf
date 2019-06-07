package main
import (
    "fmt"
    "net/http"
    "log"
)

func indexHandler(resp http.ResponseWriter, req *http.Request) {

}


func main() {
    fmt.Println("Server is listening...")
    http.HandleFunc("/", indexHandler)
    err := http.ListenAndServe("0.0.0.0:8080", nil)
    if err != nil {
        log.Fatal("ListenAndServe: ", err)
    }
}
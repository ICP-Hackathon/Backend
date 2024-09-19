package main

import (
	"encoding/json"
	"fmt"
	"net/http"
)

func main() {
	http.HandleFunc("/movecall/new_ragcoon_stage", func(w http.ResponseWriter, r *http.Request) {
		res := NewRagcoonStage()

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(res)
	})

	http.HandleFunc("/movecall/add_creator", func(w http.ResponseWriter, r *http.Request) {
		ragcoonStageId := r.URL.Query().Get("ragcoonStageId")
		fmt.Println("ragcoonStagedID", ragcoonStageId)
		creatorAddress := r.URL.Query().Get("creatorAddress")
		fmt.Println("creatorAddress", creatorAddress)
		res := AddCreator(ragcoonStageId, creatorAddress)

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(res)
	})

	http.HandleFunc("/movecall/add_consumer", func(w http.ResponseWriter, r *http.Request) {
		ragcoonStageId := r.URL.Query().Get("ragcoonStageId")
		consumerAddress := r.URL.Query().Get("consumerAddress")
		res := AddConsumer(ragcoonStageId, consumerAddress)

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(res)
	})

	http.HandleFunc("/movecall/add_ai", func(w http.ResponseWriter, r *http.Request) {
		ragcoonStageId := r.URL.Query().Get("ragcoonStageId")
		creatorAddress := r.URL.Query().Get("creatorAddress")
		AIID := r.URL.Query().Get("AIID")
		res := AddAI(ragcoonStageId, creatorAddress, AIID)

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(res)
	})

	http.HandleFunc("/movecall/add_blob_id", func(w http.ResponseWriter, r *http.Request) {
		ragcoonStageId := r.URL.Query().Get("ragcoonStageId")
		creatorAddress := r.URL.Query().Get("creatorAddress")
		AIID := r.URL.Query().Get("AIID")
		blobID := r.URL.Query().Get("blobID")
		res := AddBlob(ragcoonStageId, creatorAddress, AIID, blobID)

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(res)
	})

	http.HandleFunc("/movecall/pay_usage", func(w http.ResponseWriter, r *http.Request) {
		ragcoonStageId := r.URL.Query().Get("ragcoonStageId")
		creatorAddress := r.URL.Query().Get("creatorAddress")
		AIID := r.URL.Query().Get("AIID")
		consumerAddress := r.URL.Query().Get("consumerAddress")
		amount := r.URL.Query().Get("amount")
		res := PayUsage(ragcoonStageId, creatorAddress, AIID, consumerAddress, amount)

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(res)
	})

	http.HandleFunc("/movecall/add_recharge", func(w http.ResponseWriter, r *http.Request) {
		ragcoonStageId := r.URL.Query().Get("ragcoonStageId")
		consumerAddress := r.URL.Query().Get("consumerAddress")
		coinObjectId := r.URL.Query().Get("coinObjectId")
		res := AddRecharge(ragcoonStageId, consumerAddress, coinObjectId)

		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(res)
	})

	// // 서버 실행
	fmt.Println("Server is listening on port 8080...")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		fmt.Println("Error starting server:", err)
	}

}

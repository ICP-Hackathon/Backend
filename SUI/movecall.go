package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/block-vision/sui-go-sdk/constant"
	"github.com/block-vision/sui-go-sdk/models"
	"github.com/block-vision/sui-go-sdk/signer"
	"github.com/block-vision/sui-go-sdk/sui"
	"github.com/joho/godotenv"
)

func MoveCall(
	// packageObjectId string,
	// module string,
	function string,
	typeArguments []interface{},
	arguments []interface{},
) *models.SuiTransactionBlockResponse {
	err := godotenv.Load()
	if err != nil {
		log.Fatalf("Error loading .env file")
	}

	var ctx = context.Background()
	var cli = sui.NewSuiClient(constant.BvTestnetEndpoint)

	mnemonic := os.Getenv("MNEMONIC")
	signerAccount, err := signer.NewSignertWithMnemonic(mnemonic)

	if err != nil {
		fmt.Println(err.Error())
		return nil
	}

	fmt.Printf("signerAccount.Address: %s\n", signerAccount.Address)

	gasObj := "0x71434fc47595c28e2a361d579e58d4f9b3931daa879398f1c4ad67ab1e04e7a7"

	packageObjectId := "0xf8ecfb330ca0b55f8ffc4954b174c08b2df88c28b1e374bf4558a340683b3c86"
	module := "ragcoon"

	rsp, err := cli.MoveCall(ctx, models.MoveCallRequest{
		Signer:          signerAccount.Address,
		PackageObjectId: packageObjectId,
		Module:          module,
		Function:        function,
		// TypeArguments:   []interface{}{},
		TypeArguments: typeArguments,
		Arguments:     arguments,
		Gas:           gasObj,
		GasBudget:     "100000000",
	})

	if err != nil {
		fmt.Println(err.Error())
		return nil
	}

	// see the successful transaction url: https://explorer.sui.io/txblock/CD5hFB4bWFThhb6FtvKq3xAxRri72vsYLJAVd7p9t2sR?network=testnet
	rsp2, err := cli.SignAndExecuteTransactionBlock(ctx, models.SignAndExecuteTransactionBlockRequest{
		TxnMetaData: rsp,
		PriKey:      signerAccount.PriKey,
		// only fetch the effects field
		Options: models.SuiTransactionBlockOptions{
			ShowInput:    true,
			ShowRawInput: true,
			ShowEffects:  true,
		},
		RequestType: "WaitForLocalExecution",
	})

	if err != nil {
		fmt.Println(err.Error())
		return nil
	}
	// utils.PrettyPrint(rsp2)
	return &rsp2
}

func NewRagcoonStage() *models.SuiTransactionBlockResponse {

	res := MoveCall("new_ragcoon_stage", []interface{}{}, []interface{}{})
	return res
}

func AddCreator(ragcoonStageId string, creatorAddress string) *models.SuiTransactionBlockResponse {
	res := MoveCall("add_creator", []interface{}{}, []interface{}{ragcoonStageId, creatorAddress})
	return res
}

func AddConsumer(ragcoonStageId string, consumerAddress string) *models.SuiTransactionBlockResponse {
	res := MoveCall("add_consumer", []interface{}{}, []interface{}{ragcoonStageId, consumerAddress})
	return res
}

func AddAI(ragcoonStageId string, creatorID string, AIID string) *models.SuiTransactionBlockResponse {
	res := MoveCall("add_ai", []interface{}{}, []interface{}{ragcoonStageId, creatorID, AIID})
	return res
}

func AddBlob(ragcoonStageId string, creatorID string, AIID string, blobID string) *models.SuiTransactionBlockResponse {
	res := MoveCall("add_blob_id", []interface{}{}, []interface{}{ragcoonStageId, creatorID, AIID, blobID})
	return res
}

func PayUsage(ragcoonStageId string, creatorID string, AIID string, consumerID string, amount uint64) *models.SuiTransactionBlockResponse {
	res := MoveCall("pay_usage", []interface{}{}, []interface{}{ragcoonStageId, creatorID, AIID, consumerID, amount})
	return res
}

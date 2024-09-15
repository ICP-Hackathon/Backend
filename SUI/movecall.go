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
	packageObjectId string,
	module string,
	function string,
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

	rsp, err := cli.MoveCall(ctx, models.MoveCallRequest{
		Signer: signerAccount.Address,
		// PackageObjectId: "0x0252927bfd6eb72291b39549efbe349ef7c81c427d58009ce1a50343d5a3636c",
		// Module:          "ragcoon",
		// Function:        "new_ragcoon_stage",
		PackageObjectId: packageObjectId,
		Module:          module,
		Function:        function,
		TypeArguments:   []interface{}{},
		// Arguments:       []interface{}{ },
		Arguments: arguments,
		Gas:       gasObj,
		GasBudget: "100000000",
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
	packageObjectId := "0x0252927bfd6eb72291b39549efbe349ef7c81c427d58009ce1a50343d5a3636c"
	module := "ragcoon"

	res := MoveCall(packageObjectId, module, "new_ragcoon_stage", []interface{}{})
	return res
}

func AddCreator(ragcoonStageId string, creatorAddress string) *models.SuiTransactionBlockResponse {
	packageObjectId := "0x0252927bfd6eb72291b39549efbe349ef7c81c427d58009ce1a50343d5a3636c"
	module := "ragcoon"

	res := MoveCall(packageObjectId, module, "add_creator", []interface{}{ragcoonStageId, creatorAddress})
	return res
}

func AddConsumer(ragcoonStageId string, consumerAddress string) *models.SuiTransactionBlockResponse {
	packageObjectId := "0x0252927bfd6eb72291b39549efbe349ef7c81c427d58009ce1a50343d5a3636c"
	module := "ragcoon"

	res := MoveCall(packageObjectId, module, "add_consumer", []interface{}{ragcoonStageId, consumerAddress})
	return res
}

func AddAI(ragcoonStageId string, creatorID string, AIID string) *models.SuiTransactionBlockResponse {
	packageObjectId := "0x0252927bfd6eb72291b39549efbe349ef7c81c427d58009ce1a50343d5a3636c"
	module := "ragcoon"

	res := MoveCall(packageObjectId, module, "add_ai", []interface{}{ragcoonStageId, creatorID, AIID})
	return res
}

func AddBlob(ragcoonStageId string, creatorID string, AIID string, blobID string) *models.SuiTransactionBlockResponse {
	packageObjectId := "0x0252927bfd6eb72291b39549efbe349ef7c81c427d58009ce1a50343d5a3636c"
	module := "ragcoon"

	res := MoveCall(packageObjectId, module, "add_blob_id", []interface{}{ragcoonStageId, creatorID, AIID, blobID})
	return res
}

func PayUsage(ragcoonStageId string, creatorID string, AIID string, consumerID string, amount uint64) *models.SuiTransactionBlockResponse {
	packageObjectId := "0x0252927bfd6eb72291b39549efbe349ef7c81c427d58009ce1a50343d5a3636c"
	module := "ragcoon"

	res := MoveCall(packageObjectId, module, "pay_usage", []interface{}{ragcoonStageId, creatorID, AIID, consumerID, amount})
	return res
}

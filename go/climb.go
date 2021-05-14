// go
package main

import (
	"syscall/js"
)

func main() {
	c := make(chan bool)
	//1. Exposing go functions/values in javascript variables.
	js.Global().Set("climb", js.FuncOf(climb))
	//2. This channel will prevent the go program to exit
	<-c
}

func climb(this js.Value, inputs []js.Value) interface{} {
	climbnum := climbinternal(inputs[0].Int())
	return climbnum
}

func climbinternal(n int) int {
	a := 1
	for a < n {
		a++
	}
	return a
}

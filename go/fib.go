// go
package main

import (
	"syscall/js"
)

func main() {
	c := make(chan bool)
	//1. Exposing go functions/values in javascript variables.
	js.Global().Set("fib", js.FuncOf(fib))
	//2. This channel will prevent the go program to exit
	<-c
}

func fib(this js.Value, inputs []js.Value) interface{} {
	fibnum := fibinternal(inputs[0].Int())
	return fibnum
}

func fibinternal(n int) int {
	if n == 0 {
		return 0
	}
	if n == 1 {
		return 1
	}
	sum := fibinternal(n-1) + fibinternal(n-2)
	return sum
}

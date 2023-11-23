package main

import (
	"fmt"
	"os"
	"runtime/pprof"
)

func main() {

	// Start profiling
	f, err := os.Create("myprogram.prof")
	if err != nil {

		fmt.Println(err)
		return

	}
	pprof.StartCPUProfile(f)
	defer pprof.StopCPUProfile()

	// Run your program here

	fmt.Println("Done!")

}

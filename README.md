# Image Stitcher
## **Project members**
    *  Mohit Tiwari                 -   2021A7PS2719G 
    *  Shaunak Ravi Nagrecha        -   2021A7PS3039G
    *  Sreekar Choudary Yadlapalli  -   2021A7PS2602G
    *  Tanishq Suresh Gholap        -   2021A7PS2728G
## 1. Problem Statement
The Image Stitcher is a Go program designed to create a collage of images. It takes a source path of images and stitches them together based on the provided parameters such as shape, rows, width, and height.

Problem Statement - 
This project Image Stitcher addresses the technical challenge of programmatically generating image collages. The objective is to implement a solution that enables users to customise collage shapes (rectangles or circles), layouts (number of rows), and employs parallel processing for efficient handling of multiple images. We have implemented this in two languages, Go and Python.

POPL Angle - 
Parallelism and Performance: The POPL (Principles of Programming Languages) angle in this project lies in the efficient utilisation of parallelism for image rendering, enhancing performance. Golang's concurrency support is leveraged to handle multiple images concurrently, optimising collage creation.

## 2. Software Architecture
The software is structured around several key types:

- `MyImage`: A custom image type that wraps the standard `image.RGBA` type.
- `Circle`: A type representing a circle, used for creating circular images.
- `Size`: A type representing the size of an image.
- `ImageShape`: A type representing the shape of an image.
- `ImagePositionAndSize`: A type representing the position and size of an image.
- `ImageCollageParameters`: A type representing the parameters for creating an image collage.

The main function of the program is `makeImageCollage`, which takes a set of parameters and a list of images, and returns a new image that is a collage of the input images.

## 3. POPL Aspects
The Go programming language is used in this project, which is statically typed and compiled. It supports concurrent programming, which is used in the `makeImageCollage` function to draw images on the background in parallel. Go's garbage collection, strong typing, and built-in testing make it a robust language for this kind of application.

1. **Strongly Typed Language:** Go is a statically typed language, which means the type of a variable is known at compile time. This is evident in the code where each variable is declared with a specific type. For example, in line 31, Image is declared as a pointer to image.RGBA.
2. **Package System:** Go uses packages for code organization and reuse. In the code, various packages are imported at the beginning (lines 3-19), such as image, image/color, image/draw, image/jpeg, log, math, os, path/filepath, sort, strconv, time, and github.com/nfnt/resize.
3. **Pointers:** Go supports pointers, allowing you to pass references to values and records within your program. This is evident in the code where pointers are used, for example, in line 31 (Image *image.RGBA).

## 4. Results

The result of running the program is a new image that is a collage of the input images. The shape, size, and arrangement of the images in the collage are determined by the parameters passed to the `makeImageCollage` function. 

In addition to the final collage image, the program also produces intermediate output images at each step of the process. These images can be useful for understanding how the collage is constructed and for debugging.

The Go and Python versions of the program produce identical output images given the same input images and parameters. This consistency is important for ensuring that the Go and Python versions of the program are functionally equivalent.

Screenshots of a performance monitor are included in the `/results` directory. These screenshots show the time taken by each version to process the same set of input images. The performance comparison can be useful for understanding the trade-offs between the Go and Python versions and for deciding which version to use for a particular task.

## 5. Potential for Future Work

There are several potential areas for future work:

- **Support for more shapes**: The current version only supports rectangular and circular images. More shapes could be added in the future. This would involve extending the `drawImage` function to handle different shapes.

- **More flexible arrangement of images**: The current version arranges images in a grid. It could be extended to support more flexible arrangements. This could involve creating a new `arrangeImages` function that takes a layout parameter.

- **Performance improvements**: The performance of the `makeImageCollage` function could potentially be improved. Here are a few areas that could be optimized:

  - **Image resizing**: The current image resizing code could be optimized. This could involve using a more efficient resizing algorithm or parallelizing the resizing process.

  - **Drawing code**: The code for drawing images on the background could be optimized. This could involve reducing the number of drawing operations or using a more efficient drawing algorithm.

  - **Concurrency**: The current version uses Go's built-in support for concurrency in the `makeImageCollage` function. However, there may be other parts of the code that could benefit from parallelization.

  - **Memory usage**: The current version could potentially use a lot of memory when processing large images. This could be improved by using more memory-efficient data structures or algorithms.

## 6. Languages Used in This Project

This project primarily uses two programming languages:

- **Go**: Go is the main language used in this project. It is used for its efficiency, strong typing, and built-in testing capabilities. Go's support for concurrent programming is particularly useful in the `makeImageCollage` function, where images are drawn on the background in parallel.

- **Python**: Python is used for some auxiliary tasks such as data processing and testing. Its simplicity and extensive library support make it a good choice for these tasks.

## 7. Considerations

The choice of Go and Python was driven by the specific needs of this project. Go's efficiency and support for concurrent programming make it ideal for the core image processing tasks. On the other hand, Python's simplicity and extensive libraries make it a good choice for auxiliary tasks. This combination allows us to leverage the strengths of both languages.

## 8. Salient Features of Go and Python

The Go programming language is used in this project, which is statically typed and compiled. It has several salient features that make it suitable for this project:

- **Concurrency**: Go has built-in support for concurrent programming, which is used in the `makeImageCollage` function to draw images on the background in parallel.

- **Garbage Collection**: Go's garbage collection feature helps manage memory automatically, reducing the chance of memory leaks.

- **Strong Typing**: Go's strong typing helps catch errors at compile time, making the code more robust.

- **Built-in Testing**: Go has built-in support for testing, which makes it easier to ensure the correctness of the code.

Python is used for some auxiliary tasks such as data processing and testing. It also has several salient features:

- **Simplicity**: Python's syntax is simple and easy to read, which makes it a good choice for auxiliary tasks.

- **Extensive Libraries**: Python has a wide range of libraries for various tasks, which can help speed up development.

- **Dynamic Typing**: Python's dynamic typing allows for more flexibility in certain situations.

- **Interpreted Language**: Python is an interpreted language, which means it can run the code line by line, making it easier to debug.
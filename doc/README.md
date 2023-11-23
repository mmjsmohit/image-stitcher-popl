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
Computational Intensity: - Image stitching, a complex task, can be computationally intensive, especially when handling numerous high-resolution images. - The need for an efficient solution to manage computational resources and execution time becomes crucial.
Choice of Programming Languages: - Initially implemented the image stitching algorithm in Python. - Instead of processing images sequentially, stitching them individually onto the final collage, implementing parallelisation improves performance by enabling simultaneous stitching of all images. - Encountered performance bottlenecks due to the Global Interpreter Lock (GIL) in Python, limiting effective parallelisation.
Transition to Go for Concurrency: - Transitioned to Go, a statically-typed language known for its concurrency support through goroutines. - Go's goroutines enable concurrent execution, addressing the limitations of Python's GIL and significantly improving performance. - The adoption of Go aligns with POPL principles by emphasizing concurrency to tackle intricate image processing tasks. - Demonstrates the advantage of using a language like Go, specifically designed for concurrent and parallel programming, in addressing real-world challenges.

While image stitching has been addressed in languages like HTML, CSS, PHP, etc., our project stands out by introducing parallelization, a novel approach to enhance computational efficiency. This strategic use of concurrent processing, especially with Go's goroutines, sets our solution apart from traditional methods.

## 2. Software Architecture

The software is structured around several key types:

- `MyImage`: A custom image type that wraps the standard `image.RGBA` type.
- `Circle`: A type representing a circle, used for creating circular images.
- `Size`: A type representing the size of an image.
- `ImageShape`: A type representing the shape of an image.
- `ImagePositionAndSize`: A type representing the position and size of an image.
- `ImageCollageParameters`: A type representing the parameters for creating an image collage.

The main function of the program is `makeImageCollage`, which takes a set of parameters and a list of images, and returns a new image that is a collage of the input images.

For the Go code, we have used the nfnt/resize library (https://github.com/nfnt/resize) by and the Python Imaging Library (PIL) for the python code.
nfnt/resize -
The nfnt/resize library is a versatile Go package designed for image resizing, offering a range of interpolation methods for optimal results. With functions like resize.Resize and resize.Thumbnail, developers can efficiently scale and downscale images while preserving aspect ratios. The library supports interpolation techniques such as Nearest-Neighbor, Bilinear, Bicubic, and others, allowing users to choose the method that best suits their use case. Despite being no longer actively updated, it remains a reliable tool for image manipulation in Go.

PIL-
The Python Imaging Library (PIL), now known as the Pillow library, is a powerful image processing library in Python. PIL provides extensive support for opening, manipulating, and saving various image file formats. It offers a wide range of image processing capabilities, including resizing, cropping, filtering, and enhancing images. PIL has been important for image-related tasks, hence we chose it for this projects. Its successor, Pillow, continues to be actively maintained and expanded, ensuring compatibility with the latest Python versions and providing users with a robust set of tools for image manipulation.

In creating our image collage project, we've put together different pieces to make everything work smoothly. We used existing tools like the nfnt/resize library in Go and the Python Imaging Library (PIL) to handle some parts of dealing with images. However, the main chunk of our code, where we stitch images, figure out the layout of the collage, and make everything happen at the same time (parallelization), is our own creation. We wrote specific instructions for our project needs, making sure everything fits together well. This customized approach helped us tackle the unique challenges our project presented and ensured that all the different parts work seamlessly to generate image collages.

<img width="595" alt="image" src="https://github.com/mmjsmohit/image-stitcher-popl/assets/65406090/6f1df700-7944-43d7-ae14-786f703cf5c0">


## 3. POPL Aspects

The Go programming language is used in this project, which is statically typed and compiled. It supports concurrent programming, which is used in the `makeImageCollage` function to draw images on the background in parallel. Go's garbage collection, strong typing, and built-in testing make it a robust language for this kind of application.

1. **Strongly Typed Language:** Go is a statically typed language, which means the type of a variable is known at compile time. This is evident in the code where each variable is declared with a specific type. For example, in line 31, Image is declared as a pointer to image.RGBA.
2. **Package System:** Go uses packages for code organization and reuse. In the code, various packages are imported at the beginning (lines 3-19), such as image, image/color, image/draw, image/jpeg, log, math, os, path/filepath, sort, strconv, time, and github.com/nfnt/resize.
3. **Pointers:** Go supports pointers, allowing you to pass references to values and records within your program. This is evident in the code where pointers are used, for example, in line 31 (Image \*image.RGBA).

4. **Concurrency**: Go, the statically typed and compiled language used in this project, has built-in support for concurrent programming. This feature is utilized in the `makeImageCollage` function to draw images on the background in parallel.

5. **Garbage Collection**: Go's garbage collection feature helps manage memory automatically, reducing the chance of memory leaks. This makes it a robust language for applications like this.

6. **Strong Typing**: Go is a strongly typed language, meaning the type of a variable is known at compile time. This feature helps catch errors at compile time, making the code more robust. An example from the code is the declaration of Image as a pointer to image.RGBA at line 31.

7. **Built-in Testing**: Go has built-in support for testing, which makes it easier to ensure the correctness of the code.

8. **Package System**: Go uses packages for code organization and reuse. Various packages such as image, image/color, image/draw, image/jpeg, log, math, os, path/filepath, sort, strconv, time, and github.com/nfnt/resize are imported in the code.

9. **Pointers**: Go supports pointers, allowing references to values and records to be passed within the program. This is evident in the code where pointers are used, for example, in line 31 (Image \*image.RGBA).

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

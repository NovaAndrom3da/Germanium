# <strong>This software is UNRELEASED!</strong>
This means that there will be bugs and issues that will pop up
frequently. There are no guarantees that any of this will work
or work as intended. Although programming help is appreciated,
please be understanding that this language is still in it's
alpha stages.

# ⚗ Germanium
Germanium is an open source, dynamically typed language written
in python. It focuses on runtime speed, user readability, and
cross-compatibility. It offers both a compiled and Just-In-Time
system.

## 🤨 Why Germanium?
Germanium is written in a way to be easily minified and quickly
processed. It is also written to improve program developers' 
experiences with programming by providing an easy-to-write but
feature-filled language.

## 🔬 Getting Started
```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/Froggo8311/Germanium/main/tools/web-install.sh)"
```
Using either the prebuilt or the source versions will be different
for each setup. The compiled interpereter will be more efficient
in terms of speed, but the source build is useful for Germanium
development, allowing the develeoper to quickly change and run the
program without having to wait for a build to finish. If you choose to
use the compiled version, you can download a prebuilt version for
your operating system and architecture if available, or build from
source.

### 🔭 Build from Source (Compiled)
You can build from source using the tools provided in the 
`install_src.py` file.

#### Prebuilt
Prebuilt packages coming soon. At the moment, only the source version
is available.



### 🧪 Run from Source (Just-In-Time)
For source builds, we reccommend using the
[latest version of PyPy](https://www.pypy.org/download.html)
for the best results and speed, but CPython will also work.
<strong>Make sure you are using the correct one when running the
install script, unless you are building from source.</strong>

## ⌨ Examples
### 🌎 Hello, World!
```ge
~ This is a comment
print("Hello, World!");
```

### ➰ Functions & Return Statements
```ge
func myFunc(a as Bool = true) {
  if (a) {
    return "Yes";
  } else {
    return "No";
  }
}

print(myFunc(true)); ~ "Yes"
print(myFunc(false)); ~ "No"
```

### ➿ Loops
```ge
func loop() {
  while (true) {
    print("This only runs once.");
    break;
  }
  
  myList = ["a", "b", "c", 1, 2, 3];
  for (i in myList) {
    print(i); ~ Prints:  0  1  2  3  4  5
    print(myList[i]); ~ Prints:  a  b  c  1  2  3
  }
}
```


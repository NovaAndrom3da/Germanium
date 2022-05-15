# ⚗ Germanium
Germanium is an open source, dynamically typed language written
in python. It focuses on runtime speed, user readability, and
cross-compatibility. It offers both a compiled and Just-In-Time
system.


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
func main() {
  print("Hello, world!");
  if (__version__ == "0.0.0") {
    print("Germanium is not yet released!");
  } elif (True == False) {
    print("True equals false????");
  } else {
    print("Germanium is released!");
  }
  return "Hello there";
}

print(main()); ~ "Returns Hello there"
```


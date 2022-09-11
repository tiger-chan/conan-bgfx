from conans import ConanFile, tools
from conan.tools.cmake import CMakeToolchain, CMake, CMakeDeps


class BgfxConan(ConanFile):
    name            = "bgfx"
    version         = "1.115.8266-06b9950"
    """Tag from bgfx.cmake repo"""
    description     = "Conan package for bgfx."
    url             = "https://github.com/bkaradzic/bgfx"
    license         = "BSD"
    settings        = "arch", "build_type", "compiler", "os"
    options         = {
        "shared": [True, False],
        "multithreaded": [True, False],
        "build_tools": [True, False]
    }
    default_options = {
        "shared": False,
        "multithreaded": True,
        "build_tools": False
    }

    def source(self):
        git = tools.Git(folder=".")
        version = "v" + self.version
        try:
            git.checkout(version)
        except:
            git.clone("https://github.com/bkaradzic/bgfx.cmake.git", branch=version)

        git.run("submodule update --init --recursive")

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()

        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        variables = {
            "BUILD_SHARED_LIBS": self.options.shared,
            "BGFX_CONFIG_MULTITHREADED": self.options.multithreaded,
            "BGFX_BUILD_EXAMPLES": False,
            "BGFX_BUILD_TOOLS": self.options.build_tools,
            "BGFX_OPENGL_VERSION": 33
        }

        cmake.configure(variables=variables)
        cmake.build()
        if self.options.build_tools:
            cmake.build(target="shaderc")

    def collect_headers(self, include_folder):
        self.copy("*.h"  , dst="include", src=include_folder)
        self.copy("*.hpp", dst="include", src=include_folder)
        self.copy("*.inl", dst="include", src=include_folder)

    def package(self):
        self.collect_headers("bgfx/include")
        self.collect_headers("bimg/include")
        self.collect_headers("bx/include"  )
        self.copy("*.a"  , dst="lib", keep_path=False)
        self.copy("*.so" , dst="lib", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.exe", dst="bin", keep_path=False)
        self.copy("shaderc", dst="bin")
        if self.options.build_tools:
            self.copy("*.sh", dst="src", src="bgfx/src", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["bgfx", "bimg", "bx"]
        self.cpp_info.libs.extend(["astc-codec", "astc", "edtaa3", "etc1", "etc2", "iqa", "squish", "pvrtc", "tinyexr"])
        if self.settings.os != "Switch":
            self.cpp_info.libs.extend(["nvtt"])
        if self.settings.os == "Macos":
            self.cpp_info.exelinkflags = ["-framework Cocoa", "-framework QuartzCore", "-framework OpenGL", "-weak_framework Metal"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(["GL", "X11", "pthread", "dl"])
        if self.settings.os == "Windows":
            self.cpp_info.includedirs = ["include", "include/compat/msvc"]

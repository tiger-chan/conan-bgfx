import os

from conans import ConanFile, CMake, tools


class BgfxTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
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

    def build(self):
        cmake = CMake(self)
        # Current dir is "test_package/build/<build_id>" and CMakeLists.txt is
        # in "test_package"
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy('*.so*', dst='bin', src='lib')

    def test(self):
        if not tools.cross_building(self.settings):
            os.chdir("bin")
            if self.settings.os == "Windows":
                self.run(".%sbgfx_test.exe" % os.sep)
            else:
                self.run(".%sbgfx_test" % os.sep)

    def configure(self):
        self.options["bgfx"].build_tools = True

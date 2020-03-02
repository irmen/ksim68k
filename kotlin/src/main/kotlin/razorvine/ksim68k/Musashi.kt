package razorvine.ksim68k

import com.sun.jna.*
import com.sun.jna.Library


interface Musashi: Library {

    companion object {
        init {
            if(!Platform.isWindows())
                System.setProperty("jna.library.path", "/usr/local/lib")
        }

        val INSTANCE: Musashi by lazy { Native.load("musashi", Musashi::class.java) }

//        init {
//            val library = NativeLibrary.getInstance("/usr/local/lib/libbinaryen.so")
//            Native.register(Binaryen::class.java, library)
//        }
    }

    // functions:
    // TODO
    fun testmethod(): Boolean {
        return false
    }
}

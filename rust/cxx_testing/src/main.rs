autocxx::include_cpp! {
    #include "external/cpr/include/cpr/cpr.h"
    generate!("cpr")
    safety!(unsafe)
}


fn main() {
    println!("Hello, world!");
}

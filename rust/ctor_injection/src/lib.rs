#[ctor::dtor]
fn entry() {
    // println!("test1");
    unsafe {
        libc::printf("Hello, world!\n\0".as_ptr() as *const i8);
    }
}

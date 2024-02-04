fn add<T: std::ops::Add<Output = T>>(a: T, b: T) -> T {
    a + b
}


fn main() {
    println!("add at {:p}", add::<u32> as *const ());
    println!("added = {}", add(100, 100));

    println!("test");
    println!("Hello, world!");
}

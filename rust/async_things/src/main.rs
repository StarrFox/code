async fn a() {
    println!("a");
}

async fn b() {
    println!("b");
}

async fn async_main() {
    futures::join!(a(), b());
}

fn main() {
    futures::executor::block_on(async_main())
}

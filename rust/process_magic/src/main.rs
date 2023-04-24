use process_memory::{Memory, TryIntoProcessHandle};

fn main() {
    let test = 100;

    let self_handle = (std::process::id() as process_memory::Pid)
        .try_into_process_handle()
        .unwrap();

    let test_member: process_memory::DataMember<u32> =
        process_memory::DataMember::new_offset(self_handle, vec![&test as *const _ as usize]);

    println!("Read: {}", unsafe { test_member.read().unwrap() });
}

fn main() {}

#[no_mangle]
pub extern "C" fn fib(n: u32) -> u64 {
    match n{
        0 => 0,
        1 => 1,
        _ => fib(n-1) + fib(n-2)
    }
}

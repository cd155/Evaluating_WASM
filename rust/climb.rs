fn main() {}

#[no_mangle]
pub extern "C" fn climb(n: u32) -> u32 {
    let mut a = 0;
    while a < n{
        a += 1
    }
    return a
}

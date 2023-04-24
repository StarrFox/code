macro_rules! variadic_op {
    ($op:tt, $x:expr) => ($x);
    ($op:tt, $x:expr, $($rest:expr),+) => (variadic_op!($op, $($rest),+) $op $x);
}

macro_rules! weird_math {
    (/ $($v:expr)+) => {{
        let values = vec![$($v),+];
        values.into_iter().reduce(|a, b| a / b).unwrap()
    }};
    ($op:tt $($rest:expr)+) => (variadic_op!($op, $($rest),+));
}

fn main() {
    let added = weird_math!(+ 2 2 2);
    let subbed = weird_math!(- 2 2 2);
    println!("added: {added}, subbed: {subbed}");
}

#[cfg(test)]
mod tests {
    #[test]
    fn test_weird_math_add() {
        let added = weird_math!(+ 2 2 2);
        assert_eq!(added, 2 + 2 + 2);
    }

    #[test]
    fn test_weird_math_sub() {
        let subbed = weird_math!(- 2 3 2);
        assert_eq!(subbed, 2 - 3 - 2);
    }

    #[test]
    fn test_weird_math_add_single_value() {
        let added = weird_math!(+ 5);
        assert_eq!(added, 5);
    }

    #[test]
    fn test_weird_math_sub_single_value() {
        let subbed = weird_math!(-5);
        assert_eq!(subbed, 5);
    }

    #[test]
    fn test_weird_math_mul() {
        let multiplied = weird_math!(* 2 2 2);
        assert_eq!(multiplied, 2 * 2 * 2);
    }

    #[test]
    fn test_weird_math_div() {
        let divided = weird_math!(/ 8 2 2);
        assert_eq!(divided, 8 / 2 / 2);
    }

    #[test]
    fn test_weird_math_mul_single_value() {
        let multiplied = weird_math!(*5);
        assert_eq!(multiplied, 5);
    }

    #[test]
    fn test_weird_math_div_single_value() {
        let divided = weird_math!(/ 5);
        assert_eq!(divided, 5);
    }
}

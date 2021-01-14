@a = common global i32 0, align 4
@b = common global i32 0, align 4
define i32 @main(){
  store i32 10, i32* @a, align 4
  store i32 1, i32* @b, align 4
  %1 = load i32, i32* @a, align 4
  %2 = load i32, i32* @b, align 4
  %3 = icmp sgt i32 %1, %2
  br i1 %3, label %4, label %7
  4:
  %5 = load i32, i32* @a, align 4
  %6 = add nsw i32 %5, 1
  store i32 %6, i32* @a, align 4
  br label %7
  7:
  ret i32 0
}

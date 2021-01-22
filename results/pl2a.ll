@.str = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@n = common global i32 0, align 4
define i32 @fact(i32){
  %2 = alloca i32, align 4
  %3 = alloca i32, align 4
  store i32 %0, i32* %3, align 4
  %4 = load i32, i32* %2, align 4
  %5 = icmp sle i32 %4, 0
  br i1 %5, label %6, label %7
  6:
  store i32 1, i32* %2, align 4
  br label %13
  7:
  %8 = load i32, i32* %2, align 4
  %9 = sub nsw i32 %8, 1
  %10 = call i32 @fact(i32 %9)
  %11 = load i32, i32* %2, align 4
  %12 = mul nsw i32 %10, %11
  store i32 %12, i32* %2, align 4
  br label %13
  13:
  %14 = load i32, i32* %2, align 4
  ret i32 %14
}
define i32 @main(){
  %1 = call i32 (i8*, ...) @scanf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32* @n)
  %2 = load i32, i32* @n, align 4
  %3 = call i32 @fact(i32 %2)
  %4 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([3 x i8], [3 x i8]* @.str, i64 0, i64 0), i32 %3)
  ret i32 %0
}
declare i32 @scanf(i8*, ...)
declare i32 @printf(i8*, ...)

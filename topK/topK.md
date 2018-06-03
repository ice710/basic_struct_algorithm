# topK
---
## 一、 方法
- 1.堆排序：维护大小为k的堆，时间复杂度为 $O(nlogk)$
- 2.类快速排序：平均时间复杂度 $O(klogn)$ ,最坏时间复杂度$O(n^2)$
- 3.BFPRT算法: 最坏时间复杂度 $O(n)$

## 二、BFPRT算法

- 1.BFPRT算法步骤如下：
  - （1）选取主元；
    - （1.1）将n个元素划分为 $\lfloor \frac{n}{5} \rfloor$ 个组，每组5个元素，若有剩余，舍去；
    - （1.2）使用插入排序找到 $\lfloor \frac{n}{5} \rfloor$ 个组中每一组的中位数；
    - （1.3）对于（1.2）中找到的所有中位数，调用BFPRT算法求出它们的中位数，作为主元；
  - （2）以（1.3）选取的主元为分界点，把小于主元的放在左边，大于主元的放在右边；
  - （3）判断主元的位置与k的大小，有选择的对左边或右边递归。
- 2.执行过程：
![BFPRT](https://github.com/ice710/basic_struct_algorithm/blob/master/topK/img/BFPRT.png)
- 3.时间复杂度分析：
BFPRT算法在最坏情况下的时间复杂度是$O(n)$，下面予以证明。令 $T(n)$ 为所求的时间复杂度，则有：
$T(n)≤T(\frac{n}{5})+T(\frac{7n}{10})+c⋅n$ (c为一个正常数)
其中：
  - （1）$T(\frac{n}{5})$ 来自GetPivotIndex()，n个元素，5个一组，共有 $\frac{n}{5}$ 个中位数；
  - （2）$T(\frac{7n}{10})$ 来自BFPRT()，在 $\frac{n}{5}$ 个中位数中，主元x大于其中
$\frac{1}{2}⋅\frac{n}{5}=\frac{n}{10}$ 的中位数，而每个中位数在其本来的5个数的小组中
又大于或等于其中的3个数，所以主元x至少大于所有数中的 $\frac{n}{10}⋅{3}=\frac{3n}{10}$ 个。
即划分之后，任意一边的长度至少为 $\frac{3}{10}$，在最坏情况下，每次选择都选到了
$\frac{7}{10}$ 的那一部分。
  - （3）$c⋅n$来自其它操作，比如InsertSort()，以及GetPivotIndex()和Partition()里
所需的一些额外操作。
  - 设 $T(n)=t⋅n$，其中t为未知，它可以是一个正常数，也可以是一个关于n的函数，代入上式：
  $$t.n \le \frac{t.n}{5} + \frac{7t.n}{10} + c.n$$
  $$t \le \frac{t}{5} + \frac{7t}{10} + c$$
  $$t \le 10c$$
  (两边消去n)(再化简)(c为一个正常数)
  其中c为一个正常数，故t也是一个正常数，即$T(n)≤10c⋅n$，因此$T(n)=O(n)$，至此证明结束。

  接下来的更有意思的话题就是BFPRT算法为何选5作为分组基准，为何不是2,3,7,9呢？
  首先排除偶数，对于偶数我们很难取舍其中位数，而奇数很容易。
  再者对于3而言，会有 $T(n)≤T(\frac{n}{3})+T(\frac{2n}{3})+c⋅n$，它本身还是操作了n个元素，与以5为基准的 $\frac{9n}{10}$ 相比，其复杂度并没有减少。
  对于，7，9，...而言，对于上式中的10c，其整体都会增加，所以与5相比，5更适合。


4. 代码
```C++
/**
* BFPRT算法（前K小数问题）
*
*/

#include<iostream>
#include<algorithm>
using namespace std;

int InsertSort(int  array[], int left, int right);                 //插入排序，返回中位数下标
int GetPivotIndex(int  array[], int left, int right);              //返回中位数的中位数下标
int Partition(int array[], int left, int right, int pivot_index);  //利用中位数的中位数的下标进行划分，返回分界线下标
int BFPRT(int array[], int left, int right, const int & k);        //求第k小，返回其位置的下标

int main()
{
    int k = 5;
    int array[10] = { 1,1,2,3,1,5,-1,7,8,-10 };

    cout << "原数组：";
    for (int i = 0; i < 10; i++)
        cout << array[i] << " ";
    cout << endl;

    cout << "第" << k << "小值为：" << array[BFPRT(array, 0, 9, k)] << endl;

    cout << "变换后的数组：";
    for (int i = 0; i < 10; i++)
        cout << array[i] << " ";
    cout << endl;

    return 0;
}

/* 插入排序，返回中位数下标 */
int InsertSort(int array[], int left, int right)
{
    int temp;
    int j;
    for (int i = left + 1; i <= right; i++)
    {
        temp = array[i];
        j = i - 1;
        while (j >= left && array[j] > temp)
            array[j + 1] = array[j--];
        array[j + 1] = temp;
    }

    return ((right - left) >> 1) + left;
}

/* 返回中位数的中位数下标 */
int GetPivotIndex(int array[], int left, int right)
{
    if (right - left < 5)
        return InsertSort(array, left, right);

    int sub_right = left - 1;
    for (int i = left; i + 4 <= right; i += 5)
    {
        int index = InsertSort(array, i, i + 4);  //找到五个元素的中位数的下标
        swap(array[++sub_right], array[index]);   //依次放在左侧
    }

    return BFPRT(array, left, sub_right, ((sub_right - left + 1) >> 1) + 1);
}

/* 利用中位数的中位数的下标进行划分，返回分界线下标 */
int Partition(int array[], int left, int right, int pivot_index)
{
    swap(array[pivot_index], array[right]);  //把基准放置于末尾

    int divide_index = left;  //跟踪划分的分界线
    for (int i = left; i < right; i++)
    {
        if (array[i] < array[right])
            swap(array[divide_index++], array[i]);  //比基准小的都放在左侧
    }

    swap(array[divide_index], array[right]);  //最后把基准换回来
    return divide_index;
}

int BFPRT(int array[], int left, int right, const int & k)
{
    int pivot_index = GetPivotIndex(array, left, right);            //得到中位数的中位数下标
    int divide_index = Partition(array, left, right, pivot_index);  //进行划分，返回划分边界
    int num = divide_index - left + 1;
    if (num == k)
        return divide_index;
    else if (num > k)
        return BFPRT(array, left, divide_index - 1, k);
    else
        return BFPRT(array, divide_index + 1, right, k - num);
}
```

��                                                                        "     $     &     (     +  k   <  )   �  ;  �  M        \  O   b  I  �     �  /     "   I  V   l  )   �  >   �  !   ,     N     \  ]  l     �     �     �     �     �     �     �     �     �     �     �     �     �     �  r   	  =   w	  8  �	  K   �
     :  K   G  ;  �     �  ,   �  %     j   =  (   �  0   �  (        +     9   1 1! 2 3 3! 4 5 6 6! 7 8 9 9! A classic sudoku About the mathematics of sudoku, you can get it at Wiki, http://en.wikipedia.org/wiki/Mathematics_of_Sudoku How many possible puzzles in a 9x9 sudoku If we put the first number in a the position (1, 1), there are must have 9 numbers can be selected to put in. Then we put the second number in the postion (1, 2), there are must have 8 numbers can be selected to put in. So, and as it going on, we can write down the possible numbers we can select in every position: Put the number of 1-9 to every line(including x-way and y-way) and every box. Rules So the possible combinations are 9!*6!*3!*6!*3!*1!*3!*1!*1* = 4,514,807,808,000 Sudoku is a kind of puzzle game. It is one of the best way to learn logic, and at the same time, the Python language is one of the best computer language to learn logic. So, if we can combine these two kinds of tools to teach children or young men to learn logic, it will be perfect. This is why the project be done and going to. The base knowledge of sudoku The basic rules to solve a sudoku is very easy: The following is a classic sudoku: You can study what and how is sudoku in Wiki Page: http://en.wikipedia.org/wiki/Sudoku and the following is the solution for it: every line and every box can't duplicate of the number of 1-9. if we use python to caculate it:: |sudoku_init| |sudoku_result| Project-Id-Version: SudokuStudyLib 1.0
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2014-05-19 13:35+0800
PO-Revision-Date: 2014-05-21 11:56+0800
Last-Translator: LANGUAGE <LL@li.org>
Language-Team: LANGUAGE <LL@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Language: zh_CN
X-Generator: Poedit 1.6.5
 1 1! 2 3 3! 4 5 6 6! 7 8 9 9! 一个典型的数独题目 关于数独的数学知识, 你可以到下列网站来取得, http://en.wikipedia.org/wiki/Mathematics_of_Sudoku 在一个9x9 数独中, 可以组成多少种可能的游戏? 假如我们开始在位置(1, 1) 中置放一个数, 那必然是有9个可能的数字让我们选择. 然后当我要置放第二个数到位置(1, 2) 时, 那我们会有8个数字可以选择. 所以, 以此​​类推, 从上往下, 从左到右, 我们可以写下每一个位置可以被选择的数字: 将数字1-9 填到每一行(包含x-way 及y-way)及每一个3x3 区块。 基本规则 所以, 所有的组合就是9!*6!*3!*6!*3!*1!*3!*1!*1* = 4,514,807,808,000 数独(Sudoku)是一种智力游戏, 也是一种学习逻辑的最好工具. 而Python 则是世界上最好的电脑程式语言之一. 所以如果能够结合这两种工具, 来教导小孩或青少年来学习逻辑的话, 那就是最好的组合. 这就是这个专案的缘起, 也是这个专案的目标. 数独(Sudoku)基础知识 数独(Sudoku)的基本规则非常简单： 下面是一个典型的数独题目: 你可以从下列网站取得与学习数独(sudoku)的相关知识：http://en.wikipedia.org/wiki/Sudoku 下面是一个典型解出来的数独: 每行及每个区块的数字不能够重复。 假如我们使用 python 来计算时:: |sudoku_init| |sudoku_result| 
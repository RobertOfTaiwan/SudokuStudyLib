��                �      �     �     �     �     �     �     �     �     �     �                           k     )   �  ;  �     �  O   �  I  D     �  0   �  "   �  N   �  )   N  !   x     �     �  s  �     ,     .     1     3     5     8     :     <     >     A     C     E     G     J  r   f  >   �  4  	     M
  M   Z
  >  �
     �  #     %   &  U   L  (   �  (   �     �        1 1! 2 3 3! 4 5 6 6! 7 8 9 9! A classic sudoku About the mathematics of sudoku, you can get it at Wiki, http://en.wikipedia.org/wiki/Mathematics_of_Sudoku How many possible puzzles in a 9x9 sudoku If we put the first number in a the position (1, 1), there are must have 9 numbers can be selected to put in. Then we put the second number in the postion (1, 2), there are must have 8 numbers can be selected to put in. So, and as it going on, we can write down the possible numbers we can select in every position: Rules So the possible combinations are 9!*6!*3!*6!*3!*1!*3!*1!*1* = 4,514,807,808,000 Sudoku is a kind of puzzle game. It is one of the best way to learn logic, and at the same time, the Python language is one of the best computer language to learn logic. So, if we can combine these two kinds of tools to teach children or young men to learn logic, it will be perfect. This is why the project be done and going to. The base knowledge of sudoku The basic rules to solve a sudoku is very easy:: The following is a classic sudoku: You can study what is sudoku in Wiki Page: http://en.wikipedia.org/wiki/Sudoku and the following is the solution for it: if we use python to caculate it:: |sudoku_init| |sudoku_result| Project-Id-Version: SudokuStudyLib 1.0
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2014-05-14 06:19+0800
PO-Revision-Date: 2014-05-14 10:08+0800
Last-Translator: Robert J. Hwang <RobertOfTaiwan@gmail.com>
Language-Team: LANGUAGE <LL@li.org>
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Language: zh_TW
X-Generator: Poedit 1.6.5
 1 1! 2 3 3! 4 5 6 6! 7 8 9 9! 一個典型的數獨題目 關於數獨的數學知識, 你可以到下列網站來取得, http://en.wikipedia.org/wiki/Mathematics_of_Sudoku 在一個 9x9 數獨中, 可以組成多少種可能的遊戲? 假如我們開始在位置 (1, 1) 中置放一個數, 那必然是有9個可能的數字讓我們選擇. 然後當我要置放第二個數到位置 (1, 2) 時, 那我們會有8個數字可以選擇. 所以, 以此類推, 從上往下, 從左到右, 我們可以寫下每一個位置可以被選擇的數字: 基本規則 所以, 所有的組合就是  9!*6!*3!*6!*3!*1!*3!*1!*1* = 4,514,807,808,000 數獨(Sudoku)是一種智力遊戲,  也是一種學習邏輯的最好工具. 而 Python 則是世界上最好的電腦程式語言之一. 所以如果能夠結合這兩種工具, 來教導小孩或青少年來學習邏輯的話, 那就是最好的組合.  這就是這個專案的緣起, 也是這個專案的目標. 數獨(Sudoku)基礎知識 數獨遊戲的規則相當簡單:: 下面是一個典型的數獨題目: 你能夠從下列網站學習數獨相關知識: http://en.wikipedia.org/wiki/Sudoku 下面是一個典型解出來的數獨: 假如我們使用 python 來計算時:: |sudoku_init| |sudoku_result| 
package sphs.minesweeper;

public interface CellState {
  int adjacentMines();
  boolean isFlagged();
  boolean isMined();
  boolean isRevealed();
}
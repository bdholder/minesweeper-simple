package sphs.minesweeper;

public class Minesweeper {
  
  private static class Cell {
    private CellState stateObject = null;
    
    public int adjacentMines = 0;
    public boolean flagged = false;
    public boolean mined = false;
    public boolean revealed = false;
    
    public CellState state() {
      if (stateObject == null) {
        // anonymous CellState implementation
        stateObject = new CellState() {
          @Override
          public int adjacentMines() {
            checkRevealed();
            return adjacentMines;
          }
          
          @Override
          public boolean isFlagged() {
            return flagged;
          }
          
          @Override
          public boolean isMined() {
            checkRevealed();
            return mined;
          }
          
          @Override
          public boolean isRevealed() {
            return revealed;
          }
          
          private void checkRevealed() {
            if (!revealed) {
              throw new RuntimeException();
            }
          }
        }
        
      } else {
        return stateObject;
      }
    }
  }

  private final int COLUMNS;
  private final int MINES;
  private final int ROWS;
  
  private Cell[][] board;
  private boolean gameOver = false;
  private boolean initialized = false;
  private int unflaggedMines;
  private boolean victory = false;
  
  public Minesweeper(int rows, int columns, int mines) {
    ROWS = rows;
    COLUMNS = columns;
    MINES = unflaggedMines = mines;
  }
  
  private void boundsCheck(int row, int column) {
    if (row < 0 || row >= ROWS || column < 0 || column >= COLUMNS) {
      throw new IndexOutOfBoundsException();
    }
  }
  
  public void flag(int row, int column) {
    boundsCheck(row, column);
    Cell cell = board[row][column];
    cell.flagged = true;
    
    if (cell.mined) {
      //a winrar is you
      if (--unflaggedMines == 0) {
        gameOver = true;
        victory = true;
      }
    }
  }
  
  public boolean gameOver() {
    return gameOver;
  }
  
  public void reveal(int row, int column) {
    boundsCheck(row, column);
    Cell cell = board[row][column];
    cell.revealed = true;
    
    // If player blew up, reveal all mines
    if (cell.mined) {
      gameOver = true;
      for (int r = 0; r < ROWS; ++r) {
        for (int c = 0; c < COLUMNS; ++c) {
          if (board[r][c].mined) {
            board[r][c].revealed = true;
          }
        }
      }
    }
  }
  
  public CellState state(int row, int column) {
    boundsCheck(row, column);
    return board[row][column].state();
  }
  
  public boolean victory() {
    if (!gameOver) {
      return false;
    } else {
      return this.victory;
    }
  }
}
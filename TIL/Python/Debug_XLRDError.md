# Error
```python
import pandas as pd

intent = pd.read_excel('의도 데이터 _20200113_로차.xls')
```
```
---------------------------------------------------------------------------
XLRDError                                 Traceback (most recent call last)
<ipython-input-11-a016e41c6052> in <module>
----> 1 pd.read_excel('키워드 데이터 _20200113_로차.xls')

~\AppData\Local\Continuum\anaconda3\envs\basic\lib\site-packages\pandas\util\_decorators.py in wrapper(*args, **kwargs)
    206                 else:
    207                     kwargs[new_arg_name] = new_arg_value
--> 208             return func(*args, **kwargs)
    209 
    210         return wrapper

~\AppData\Local\Continuum\anaconda3\envs\basic\lib\site-packages\pandas\io\excel\_base.py in read_excel(io, sheet_name, header, names, index_col, usecols, squeeze, dtype, engine, converters, true_values, false_values, skiprows, nrows, na_values, keep_default_na, verbose, parse_dates, date_parser, thousands, comment, skip_footer, skipfooter, convert_float, mangle_dupe_cols, **kwds)
    308 
    309     if not isinstance(io, ExcelFile):
--> 310         io = ExcelFile(io, engine=engine)
    311     elif engine and engine != io.engine:
    312         raise ValueError(

~\AppData\Local\Continuum\anaconda3\envs\basic\lib\site-packages\pandas\io\excel\_base.py in __init__(self, io, engine)
    817         self._io = _stringify_path(io)
    818 
--> 819         self._reader = self._engines[engine](self._io)
    820 
    821     def __fspath__(self):

~\AppData\Local\Continuum\anaconda3\envs\basic\lib\site-packages\pandas\io\excel\_xlrd.py in __init__(self, filepath_or_buffer)
     19         err_msg = "Install xlrd >= 1.0.0 for Excel support"
     20         import_optional_dependency("xlrd", extra=err_msg)
---> 21         super().__init__(filepath_or_buffer)
     22 
     23     @property

~\AppData\Local\Continuum\anaconda3\envs\basic\lib\site-packages\pandas\io\excel\_base.py in __init__(self, filepath_or_buffer)
    357             self.book = self.load_workbook(filepath_or_buffer)
    358         elif isinstance(filepath_or_buffer, str):
--> 359             self.book = self.load_workbook(filepath_or_buffer)
    360         else:
    361             raise ValueError(

~\AppData\Local\Continuum\anaconda3\envs\basic\lib\site-packages\pandas\io\excel\_xlrd.py in load_workbook(self, filepath_or_buffer)
     34             return open_workbook(file_contents=data)
     35         else:
---> 36             return open_workbook(filepath_or_buffer)
     37 
     38     @property

~\AppData\Local\Continuum\anaconda3\envs\basic\lib\site-packages\xlrd\__init__.py in open_workbook(filename, logfile, verbosity, use_mmap, file_contents, encoding_override, formatting_info, on_demand, ragged_rows)
    155         formatting_info=formatting_info,
    156         on_demand=on_demand,
--> 157         ragged_rows=ragged_rows,
    158     )
    159     return bk

~\AppData\Local\Continuum\anaconda3\envs\basic\lib\site-packages\xlrd\book.py in open_workbook_xls(filename, logfile, verbosity, use_mmap, file_contents, encoding_override, formatting_info, on_demand, ragged_rows)
     90         t1 = perf_counter()
     91         bk.load_time_stage_1 = t1 - t0
---> 92         biff_version = bk.getbof(XL_WORKBOOK_GLOBALS)
     93         if not biff_version:
     94             raise XLRDError("Can't determine file's BIFF version")

~\AppData\Local\Continuum\anaconda3\envs\basic\lib\site-packages\xlrd\book.py in getbof(self, rqd_stream)
   1276             bof_error('Expected BOF record; met end of file')
   1277         if opcode not in bofcodes:
-> 1278             bof_error('Expected BOF record; found %r' % self.mem[savpos:savpos+8])
   1279         length = self.get2bytes()
   1280         if length == MY_EOF:

~\AppData\Local\Continuum\anaconda3\envs\basic\lib\site-packages\xlrd\book.py in bof_error(msg)
   1270 
   1271         def bof_error(msg):
-> 1272             raise XLRDError('Unsupported format, or corrupt file: ' + msg)
   1273         savpos = self._position
   1274         opcode = self.get2bytes()

XLRDError: Unsupported format, or corrupt file: Expected BOF record; found b'<meta ht'
```

# Solution
```python
intent = pd.read_html('의도 데이터 _20200113_로차.xls')
```

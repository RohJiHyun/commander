from . import serialize
from ..envhelper.env import DirectoryEnvironment

env = DirectoryEnvironment

class SerializeHelper():
    def __initialize_vars(self):
        self.input_env = None
        self.output_env = None
        
        ## __FUNCTION_OR_CLASS__ ##
        self.input_path_base_load_cls_or_func = None
        self.data_excute_cls_or_func = None
        self.tmp_store_cls_or_func = None
        self.tmp_load_cls_or_func = None
        self.output_path_base_save_cls_or_func = None


        # __INER_DATA
        self.__data = None 

        self.__compiled = False

        
    
    def __init__(self, input_env, output_env,
                 input_path_base_load_cls_or_func = None,
                 data_excute_cls_or_func = None, 
                 tmp_store_cls_or_func=None, 
                 tmp_load_cls_or_func = None,
                 output_path_base_save_cls_or_func = None
                 ):
        """
            
            OPTIONAL ARGUMENTS.
            ( path : STRING ) -> ( result : ANYTYPE ) input_path_base_load_cls_or_func : load function or class that implement __call__.
            ( result : ANYTYPE ) -> ( result : ANYTYPE ) data_excute_cls_or_func : data processing function or class that implement __call__.
            ( result : ANYTYPE ) -> ( NONE ) tmp_store_cls_or_func : store data tmporary in Variable {self.__data}. save function or class that implement __call__.
            ( result : ANYTYPE ) -> ( result : ANYTYPE ) tmp_load_cls_or_func : function that load tmporary saved data and do preprocess until return data or class that implement __call__.
            ( path : STRING, result : ANYTYPE ) -> ( NONE ) output_path_base_save_cls_or_func : load function or class that implement __call__.
            store_cls
        """
        self.__initialize_vars()
        self.set_env(input_env, output_env)
         
        self.input_path_base_load_cls_or_func = input_path_base_load_cls_or_func
        self.data_excute_cls_or_func = data_excute_cls_or_func
        self.tmp_store_cls_or_func = tmp_store_cls_or_func
        self.tmp_load_cls_or_func = tmp_load_cls_or_func
        self.output_path_base_save_cls_or_func = output_path_base_save_cls_or_func

        self.__data = None
        self.__compiled = False


    def set_env(self, input_env = None, output_env = None):
        self.input_env = input_env
        self.output_env = output_env
        return self


    def __valid_state_check(self):
        flag = False
        if self.input_env or self.output_env:
            flag = True

        return flag
    def compile(self):
        self.__data = None
        if self.__valid_state_check() :
            self.compiled = True
        return self



    def run(self):
        """
            main Method
        """
        if self.compiled : 
            raise Exception("Not compiled.")


        for dir_change_flag, path in self.input_env:
            
            result = self.__load_from_path(path)
            result = self.__excute_data_processing(result)
            self.__tmp_store(result)

            if dir_change_flag : 
                part_result = self.__tmp_load()
                self.__save_by_directory(part_result)


    # __PRIVATE__METHOD__ #

    def __load_from_path(self, path):
        """
            load from data.
        """
        val = None
        if self.input_path_base_load_cls_or_func != None and path != None:
            val = self.input_path_base_load_cls_or_func(path)
        return val
    
    def __excute_data_processing(self, data) : 
        """
            excute data processing
        """
        val = None
        if self.data_excute_cls_or_func != None and data != None:
            val = self.data_excute_cls_or_func(data)
        return val
    

    def __tmp_store(self, data):
        """
            tmp save data.
        """
        if self.tmp_store_cls_or_func != None and data != None:
            previous_data = self.__data 
            self.__data = self.tmp_store_cls_or_func(previous_data, data)
        
        

    def __tmp_load(self):
        """
            tmp saved data load preprocessing.
        """
        val = None
        if self.tmp_load_cls_or_func != None and self.__data != None:
            val = self.tmp_load_cls_or_func(self.__data)
            self.__data = None
        return val
    

    def __save_from_data(self, path, data):
        """
            final data save processing
        """
        if self.output_path_base_save_cls_or_func != None and path != None and data != None :
            self.input_path_base_load_cls_or_func(path, data)
        
        
    def __save_by_directory(self, data):
        """
            final data save processing. 
            call __save_from_data function in this function
        """
        path = self.output_env.next_category_path()
        self.__save_from_data(path, data)

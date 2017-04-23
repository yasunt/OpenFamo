class SampleClass(object):

    class_var = 'This is a class variable.'

    def instance_method(self):
        print(SampleClass.class_var)


if __name__ == '__main__':
    sc = SampleClass()
    sc.instance_method()
